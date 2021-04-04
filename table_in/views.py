from django.db.models import Q
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Sum
from django.db.models import Count
from .models import TableStat, TableUsers, UsersShtat
from .forms import ChangeStatusUsers, AddUsers
from .send_pdf import send_email
from django.views.generic import View
from .utils import ObjectUpdateMixin, ObjectDeleteMixin, render_to_pdf
from django.contrib.auth.mixins import LoginRequiredMixin
import time, os


# For pdf
from django.http import HttpResponse
from django_xhtml2pdf.utils import fetch_resources, generate_pdf
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from django.contrib import messages
# Create your views here.


def home_page(request):
    time_day = time.strftime("%d.%m.%Y", time.localtime())

    status = TableStat.objects.all()
    status_not_exist = status.exclude(Q(number=1) | Q(
        number=2)).annotate(count_names=Count('tableusers__name'))
    status_not_exist_annotate = status_not_exist.annotate(
        num_names=F('tableusers__name'))

    # В строю
    table_users_all = TableUsers.objects.all()
    v_stroyu = table_users_all.filter(user_status=1)
    v_raspor = table_users_all.filter(user_status=2)
    otsutst = table_users_all.exclude(Q(user_status=1) | Q(
        user_status=2))

    # По штату
    user_shtat = UsersShtat.objects.all()
    user_shtat_all = user_shtat.aggregate(Sum('count_shtat'))
    user_shtat_one = user_shtat.get(name=1).count_shtat
    user_shtat_two = user_shtat.get(name=2).count_shtat
    user_shtat_tree = user_shtat.get(name=3).count_shtat

    # По факту
    st_users = TableUsers.objects.all()
    st_users_all = st_users.count()
    st_users_one = st_users.filter(user_category=1).count()
    st_users_two = st_users.filter(user_category=2).count()
    st_users_tree = st_users.filter(user_category=3).count()

    # Всего по штату
    all_all = [value for key, value in user_shtat_all.items()]
    # Всего некомплект
    nekompl_all = all_all[0] - st_users_all
    # средний и старший НC некомплект
    nekompl_shtat_one = user_shtat_one - st_users_one
    # рядовой и младший НС некомлпект
    nekompl_shtat_two = user_shtat_two - st_users_two
    # служащие некомплект
    nekompl_shtat_tree = user_shtat_tree - st_users_tree

    # Подпись
    sign = TableUsers.objects.filter(users_sign=True)

    context = {
        'status': status,
        'status_not_exist': status_not_exist,
        'status_not_exist_annotate': status_not_exist_annotate,
        'sign': sign,
        'time_day': time_day,
        'v_stroyu': v_stroyu,
        'v_raspor': v_raspor,
        'otsutst': otsutst,
        'table_users_all': table_users_all,
        'st_users_all': st_users_all,
        'user_shtat_one': user_shtat_one,
        'user_shtat_two': user_shtat_two,
        'user_shtat_tree': user_shtat_tree,
        'user_shtat_all': user_shtat_all,
        'st_users_one': st_users_one,
        'st_users_two': st_users_two,
        'st_users_tree': st_users_tree,
        'nekompl_all': nekompl_all,
        'nekompl_shtat_one': nekompl_shtat_one,
        'nekompl_shtat_two': nekompl_shtat_two,
        'nekompl_shtat_tree': nekompl_shtat_tree,
    }
    return render(request, 'table_in/index.html', context)
    

class StatusChange(View):
    def get(self, request, queryset=None):
        status_us = TableUsers.objects.filter()
        status_form = ChangeStatusUsers()
        return render(request, 'table_in/status_change.html', context={'form': status_form, 'status_us': status_us})


class CreateFields(View):
    def get(self, request):
        form = AddUsers()
        return render(request, 'table_in/create_fields.html', context={'form': form})

    def post(self, request):
        bound_form = AddUsers(request.POST)

        if bound_form.is_valid():
            new_form = bound_form.save()
            return redirect(home_page)
        return render(request, 'table_in/create_fields.html', context={'form': bound_form})


def list_users(request):
    list_users_all = TableUsers.objects.all()
    sign = TableUsers.objects.filter(users_sign=True)
    return render(request, 'table_in/lists_users.html', 
                    {
                    'list_users_all': list_users_all,
                    'sign': sign,
                    }
                )


# LoginRequiredMixin,
class UsersUpdate(ObjectUpdateMixin, View):
    model = TableUsers
    model_form = AddUsers
    template = 'table_in/update_users.html'
    raise_exception = True


class UsersDelete(ObjectDeleteMixin, View):
    model = TableUsers
    template = 'table_in/delete_users.html'
    redirect_url = 'home_page'
    raise_exception = True


# PDF PREVIEW
def pdf_generate(request):
    resp = HttpResponse(content_type='application/pdf')
    
    time_day = time.strftime("%d.%m.%Y", time.localtime())

    status = TableStat.objects.all()
    status_not_exist = status.exclude(Q(number=1) | Q(
        number=2)).annotate(count_names=Count('tableusers__name'))
    status_not_exist_annotate = status_not_exist.annotate(
        num_names=F('tableusers__name'))

    # В строю
    table_users_all = TableUsers.objects.all()
    v_stroyu = table_users_all.filter(user_status=1)
    v_raspor = table_users_all.filter(user_status=2)
    otsutst = table_users_all.exclude(Q(user_status=1) | Q(
        user_status=2))

    # По штату
    user_shtat = UsersShtat.objects.all()
    user_shtat_all = user_shtat.aggregate(Sum('count_shtat'))
    user_shtat_one = user_shtat.get(name=1).count_shtat
    user_shtat_two = user_shtat.get(name=2).count_shtat
    user_shtat_tree = user_shtat.get(name=3).count_shtat

    # По факту
    st_users = TableUsers.objects.all()
    st_users_all = st_users.count()
    st_users_one = st_users.filter(user_category=1).count()
    st_users_two = st_users.filter(user_category=2).count()
    st_users_tree = st_users.filter(user_category=3).count()

    # Всего по штату
    all_all = [value for key, value in user_shtat_all.items()]
    # Всего некомплект
    nekompl_all = all_all[0] - st_users_all
    # средний и старший НC некомплект
    nekompl_shtat_one = user_shtat_one - st_users_one
    # рядовой и младший НС некомлпект
    nekompl_shtat_two = user_shtat_two - st_users_two
    # служащие некомплект
    nekompl_shtat_tree = user_shtat_tree - st_users_tree

    # Подпись
    sign = TableUsers.objects.filter(users_sign=True)

    context = {
        'status': status,
        'status_not_exist': status_not_exist,
        'status_not_exist_annotate': status_not_exist_annotate,
        'sign': sign,
        'time_day': time_day,
        'v_stroyu': v_stroyu,
        'v_raspor': v_raspor,
        'otsutst': otsutst,
        'table_users_all': table_users_all,
        'st_users_all': st_users_all,
        'user_shtat_one': user_shtat_one,
        'user_shtat_two': user_shtat_two,
        'user_shtat_tree': user_shtat_tree,
        'user_shtat_all': user_shtat_all,
        'st_users_one': st_users_one,
        'st_users_two': st_users_two,
        'st_users_tree': st_users_tree,
        'nekompl_all': nekompl_all,
        'nekompl_shtat_one': nekompl_shtat_one,
        'nekompl_shtat_two': nekompl_shtat_two,
        'nekompl_shtat_tree': nekompl_shtat_tree,
    }
    
    result = generate_pdf('table_in/index_pdf.html',
                          file_object=resp, context=context)
    return result


# PDF GENERATE AND SEND
class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        time_day = time.strftime("%d.%m.%Y", time.localtime())

        status = TableStat.objects.all()
        status_not_exist = status.exclude(Q(number=1) | Q(
            number=2)).annotate(count_names=Count('tableusers__name'))
        status_not_exist_annotate = status_not_exist.annotate(
            num_names=F('tableusers__name'))

        # В строю
        table_users_all = TableUsers.objects.all()
        v_stroyu = table_users_all.filter(user_status=1)
        v_raspor = table_users_all.filter(user_status=2)
        otsutst = table_users_all.exclude(Q(user_status=1) | Q(
            user_status=2))

        # По штату
        user_shtat = UsersShtat.objects.all()
        user_shtat_all = user_shtat.aggregate(Sum('count_shtat'))
        user_shtat_one = user_shtat.get(name=1).count_shtat
        user_shtat_two = user_shtat.get(name=2).count_shtat
        user_shtat_tree = user_shtat.get(name=3).count_shtat

        # По факту
        st_users = TableUsers.objects.all()
        st_users_all = st_users.count()
        st_users_one = st_users.filter(user_category=1).count()
        st_users_two = st_users.filter(user_category=2).count()
        st_users_tree = st_users.filter(user_category=3).count()

        # Всего по штату
        all_all = [value for key, value in user_shtat_all.items()]
        # Всего некомплект
        nekompl_all = all_all[0] - st_users_all
        # средний и старший НC некомплект
        nekompl_shtat_one = user_shtat_one - st_users_one
        # рядовой и младший НС некомлпект
        nekompl_shtat_two = user_shtat_two - st_users_two
        # служащие некомплект
        nekompl_shtat_tree = user_shtat_tree - st_users_tree

        # Подпись
        sign = TableUsers.objects.filter(users_sign=True)

        context = {
            'status': status,
            'status_not_exist': status_not_exist,
            'status_not_exist_annotate': status_not_exist_annotate,
            'sign': sign,
            'time_day': time_day,
            'v_stroyu': v_stroyu,
            'v_raspor': v_raspor,
            'otsutst': otsutst,
            'table_users_all': table_users_all,
            'st_users_all': st_users_all,
            'user_shtat_one': user_shtat_one,
            'user_shtat_two': user_shtat_two,
            'user_shtat_tree': user_shtat_tree,
            'user_shtat_all': user_shtat_all,
            'st_users_one': st_users_one,
            'st_users_two': st_users_two,
            'st_users_tree': st_users_tree,
            'nekompl_all': nekompl_all,
            'nekompl_shtat_one': nekompl_shtat_one,
            'nekompl_shtat_two': nekompl_shtat_two,
            'nekompl_shtat_tree': nekompl_shtat_tree,
        }
        # pdf = generate_pdf('table_in/index_pdf.html', context)
        date_year = f'{time.strftime("%Y", time.localtime())}'
        date_month = f'{time.strftime("%m-%Y", time.localtime())}'
        date_pdf = f'{time.strftime("%Y-%m-%d", time.localtime())}'
        name_pdf = f'{date_pdf} NAME_PDF_OF_LIST_USERS.pdf'

        link = f"url 'media/pdf/{date_year}/{date_month}/{name_pdf}' "
        if os.path.realpath(link):
            with open(link, 'wb') as output:
                template = get_template('table_in/index_pdf.html')
                html = template.render(context)
                pdf = pisa.CreatePDF(html.encode("UTF-8"),
                                    output, encoding='UTF-8', link_callback=fetch_resources)
                send_email(link, name_pdf)
                messages.success(request, 'PDF сформирован и отправлен!')
        return redirect('home_page')
        # return pdf
