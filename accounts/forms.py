from django import forms

from accounts.models import User, UserProfile
from accounts.validators import allow_only_images_validator

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password']
    
    def clean(self): # ตรวจสอบความถูกต้องของข้อมูลทั้งฟอร์ม (in general, clean() collects validated data into cleaned_data dictionary)
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
            
class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator]) # optional adjust css file input
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    
    # Way1 : readable only form (simple)
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'pin_code', 'latitude', 'longtitude']

    # Way2 : readable only form (complex and handy)
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longtitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'