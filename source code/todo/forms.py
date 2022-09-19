from django.forms import ModelForm
from .models import Todo,IMAGE_upload

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'memo', 'important']


class IMAGE_upload_form(ModelForm):
    class Meta:
        model = IMAGE_upload
        fields = ['Enter_Subject_of_received_data_to_encrypt_file','steganography_image']


