from muscn.utils.forms import HTML5BootstrapModelForm as form
from django import forms
from .models import BankDeposit, Payment, BankAccount
from apps.users.models import User


class BankDepositForm(form):
    class Meta:
        model = BankDeposit
        exclude = ('payment', )

    def __init__(self, *args, **kwargs):
        super(BankDepositForm, self).__init__(*args, **kwargs)
        self.fields['bank'].empty_label = None


class PaymentFormMixin(object):
    pass


class BankDepositPaymentForm(form):
    user = forms.ModelChoiceField(User.objects.all(), empty_label=None)
    date_time = forms.DateTimeField()
    amount = forms.FloatField()
    # verified_by = forms.ModelChoiceField(User.objects.all(), empty_label=None)
    remarks = forms.CharField(widget=forms.Textarea, required=False)

    def save(self, commit=True):
        obj = self.instance
        if not obj.payment_id:
            obj.payment = Payment()
        obj.payment.user = self.cleaned_data['user']
        obj.payment.amount = self.cleaned_data['amount']
        obj.payment.remarks = self.cleaned_data['remarks']
        obj.payment.date_time = self.cleaned_data['date_time']
        obj.payment.save()
        obj.payment_id = obj.payment.id
        return super(BankDepositPaymentForm, self).save(commit=True)


    def __init__(self, *args, **kwargs):
        super(BankDepositPaymentForm, self).__init__(*args, **kwargs)
        self.fields['bank'].empty_label = None
        if self.instance.payment_id:
            self.initial['amount'] = self.instance.payment.amount
            self.initial['date_time'] = self.instance.payment.date_time
            self.initial['user'] = self.instance.payment.user
            self.initial['remarks'] = self.instance.payment.remarks


    class Meta:
        model = BankDeposit
        exclude = ('payment', )


class PaymentForm(form):
    class Meta:
        model = Payment

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = None
        self.fields['user'].widget.choices = self.fields['user'].choices


class BankAccountForm(form):
    class Meta:
        model = BankAccount