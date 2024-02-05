from abc import ABC

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic import TemplateView, ListView, DetailView

from apps.tunduk.forms import InfocomForm, INNForm, ENICodeForm

from apps.history.models import TundukRequestLog

from utils.tunduk.infocom import Infocom
from utils.tunduk.kadastr import Kadastr
from utils.tunduk.minSelXoz import MinSelXoz
from utils.tunduk.tunduk_request_log import tunduk_request_logic
from utils.tunduk.unaa import Unaa
from utils.tunduk.minjyst import Minjyst
from utils.utils import byte_to_file


class TundukController(LoginRequiredMixin, TemplateView):
    template_name = 'tunduk/controller.html'


class PersonalInfo(LoginRequiredMixin, TemplateView):
    template_name = 'tunduk/personal_info.html'
    form = InfocomForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = InfocomForm()
        context['unaa_form'] = INNForm()
        context['eni_form'] = ENICodeForm()

        return context


class TundukAbstractList(ABC, LoginRequiredMixin, ListView):
    model = TundukRequestLog
    template_name = 'tunduk/request_list.html'

    def get_queryset(self):
        queryset = TundukRequestLog.objects.filter(
            user=self.request.user
        ).order_by('-created_at')
        return queryset


class InfocomRequestedList(TundukAbstractList):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(request_type=TundukRequestLog.RequestType.INFOCOM)
        return qs


class UnaaRequestedList(TundukAbstractList):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(request_type=TundukRequestLog.RequestType.UNAA)
        return qs


class MinjystRequestedList(TundukAbstractList):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(request_type=TundukRequestLog.RequestType.MINJYST)
        return qs


class KadastrRequestedList(TundukAbstractList):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(request_type=TundukRequestLog.RequestType.KADASTR)
        return qs


class MinSelXozRequestedList(TundukAbstractList):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(request_type=TundukRequestLog.RequestType.MINSELXOZ)
        return qs


class TundukAbstractClass(ABC, LoginRequiredMixin, DetailView):
    model = TundukRequestLog
    template_name = 'tunduk/request_detail.html'


class InfocomRequestedDetail(TundukAbstractClass):

    def post(self, request, *args, **kwargs):
        form = InfocomForm(request.POST, request.FILES)

        if form.is_valid():
            # Получение данных из СМЭВ Тундук
            infocom = Infocom('bankPinService')
            result, response = infocom.post_bankPinService(form.cleaned_data)

            if response:
                # Проверка на ошибку со стороные СМЭВ "Тундук"
                if 'faultcode' in response.text:
                    message = result.get('Ошибка', 'Результат не найден. Проверьте контакт, серию и номер')
                    messages.warning(request, message)
                    tunduk_request_logic(request,
                                         message,
                                         infocom)

                # Проверка успешности запроса
                elif response.status_code == 200:
                    tunduk_request = tunduk_request_logic(
                        request,
                        result,
                        infocom,
                        result.pop('image'),
                        full_name=f'ФИО: {result.get("surname")} {result.get("name")} {result.get("patronymic")},'
                                  f'ИНН: {result.get("pin")}',
                        wallet=True
                    )

                    return HttpResponseRedirect(reverse('tunduk:infocom-detail',
                                                        args=[tunduk_request.created_at.year,
                                                              tunduk_request.created_at.month,
                                                              tunduk_request.pk,
                                                              tunduk_request.uuid]))
            else:
                messages.warning(request, "Введите пин в X-Road Тундук")

        return HttpResponseRedirect(reverse('tunduk:tunduk-request'))


class UnaaRequestedDetail(TundukAbstractClass):
    def post(self, request, *args, **kwargs):
        form = INNForm(request.POST)
        if form.is_valid():
            # Получение данных из СМЭВ Тундук
            unaa = Unaa('transportByPin')
            result, response = unaa.postTransportByPin(form.cleaned_data)

            if response:
                # Проверка на ошибку со стороные СМЭВ "Тундук"
                if 'faultcode' in response.text:
                    message = result.get('Ошибка', 'Результат не найден. Проверьте ИНН')
                    messages.warning(request, message)
                    tunduk_request_logic(request,
                                         message,
                                         unaa)

                elif '<ts1:status>203</ts1:status>' in response.text:
                    messages.warning(request, 'Результат не найден. Проверьте ИНН')
                # Проверка успешности запроса
                elif response.status_code == 200:
                    tunduk_request = tunduk_request_logic(request, result, unaa, wallet=True)

                    return HttpResponseRedirect(reverse('tunduk:unaa-detail',
                                                        args=[tunduk_request.created_at.year,
                                                              tunduk_request.created_at.month,
                                                              tunduk_request.pk,
                                                              tunduk_request.uuid]))

            else:
                messages.warning(request, "Введите пин в X-Road Тундук")

        return HttpResponseRedirect(reverse('tunduk:tunduk-request'))


class MinjystRequestedDetail(TundukAbstractClass):
    def post(self, request, *args, **kwargs):
        form = INNForm(request.POST)
        if form.is_valid():
            # Получение данных из СМЭВ Тундук
            minjyst = Minjyst('getSubjectByTin', version=None)
            result, response = minjyst.postSubjectByTin(form.cleaned_data)

            if response:
                # Проверка на ошибку со стороные СМЭВ "Тундук"
                if 'faultcode' in response.text:
                    message = result.get('Ошибка', 'Результат не найден. Проверьте ИНН')
                    messages.warning(request, message)
                    tunduk_request_logic(request,
                                         message,
                                         minjyst)

                # Проверка успешности запроса
                elif response.status_code == 200:
                    tunduk_request = tunduk_request_logic(request, result, minjyst, wallet=True)

                    return HttpResponseRedirect(reverse('tunduk:minjyst-detail',
                                                        args=[tunduk_request.created_at.year,
                                                              tunduk_request.created_at.month,
                                                              tunduk_request.pk,
                                                              tunduk_request.uuid]))
            else:
                messages.warning(request, "Введите пин в X-Road Тундук")

        return HttpResponseRedirect(reverse('tunduk:tunduk-request'))


class KadastrRequestedDetail(TundukAbstractClass):
    def post(self, request, *args, **kwargs):
        form = ENICodeForm(request.POST)
        if form.is_valid():
            # Получение данных из СМЭВ Тундук
            kadastr = Kadastr()
            response = kadastr.getPropertyPDF(
                form.cleaned_data.get('eni_code'))
            if response:
                # Проверка на ошибку со стороные СМЭВ "Тундук"
                if 'faultcode' in response.text or not response.json().get('status'):
                    messages.warning(request, response['message'])
                    tunduk_request_logic(request,
                                         response['message'],
                                         kadastr,
                                         wallet=True)

                # Проверка успешности запроса
                elif response.status_code == 200:
                    response = response.json()
                    file = byte_to_file(response.get('response').get('image'))
                    tunduk_request = tunduk_request_logic(request,
                                                          response.get('response').get('info'),
                                                          kadastr,
                                                          file=file,
                                                          filename=response.get('response').get('name'),
                                                          wallet=True)

                    return HttpResponseRedirect(reverse('tunduk:kadastr-detail',
                                                        args=[tunduk_request.created_at.year,
                                                              tunduk_request.created_at.month,
                                                              tunduk_request.pk,
                                                              tunduk_request.uuid]))
            else:
                messages.warning(request, "Введите пин в X-Road Тундук")

        return HttpResponseRedirect(reverse('tunduk:tunduk-request'))


class MinSelXozRequestedDetail(TundukAbstractClass):

    def post(self, request, *args, **kwargs):
        form = INNForm(request.POST, request.FILES)

        if form.is_valid():
            # Получение данных из СМЭВ Тундук
            minselxoz = MinSelXoz('Data')
            result, response = minselxoz.post_animal_data_from_inn(form.cleaned_data)

            if response:
                # Проверка на ошибку со стороные СМЭВ "Тундук"
                if 'faultcode' in response.text:
                    message = result.get('Ошибка', 'Результат не найден. Проверьте ИНН')
                    messages.warning(request, message)
                    tunduk_request_logic(request,
                                         message,
                                         minselxoz)

                # Проверка успешности запроса
                elif response.status_code == 200:
                    tunduk_request = tunduk_request_logic(request, result, minselxoz, wallet=True)

                    return HttpResponseRedirect(reverse('tunduk:minselxoz-detail',
                                                        args=[tunduk_request.created_at.year,
                                                              tunduk_request.created_at.month,
                                                              tunduk_request.pk,
                                                              tunduk_request.uuid]))
            else:
                messages.warning(request, "Введите пин в X-Road Тундук")

        return HttpResponseRedirect(reverse('tunduk:tunduk-request'))
