from django import forms

from accounts.models import User
from vendor.models import Vendor


class VendorForm(forms.ModelForm):
    vendor_license = forms.ImageField(widget=forms.FileInput(attrs={'class': 'btn btn-info'})) # optional adjust css file input
    
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_license']
    
    # def clean(self): # ตรวจสอบความถูกต้องของข้อมูลทั้งฟอร์ม (in general, clean() collects validated data into cleaned_data dictionary)
    #     cleaned_data = super(UserForm, self).clean()
    #     password = cleaned_data.get('password')
    #     confirm_password = cleaned_data.get('confirm_password')

    #     if password != confirm_password:
    #         raise forms.ValidationError(
    #             "Password does not match!"
    #         )