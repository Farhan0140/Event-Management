
from django import forms
from app_admin.models import Participant, Category, Event


class For_Mixin:
    default_classes = "p-2 my-4 border rounded-lg focus:outline-none focus:border-sky-500 focus:ring-1 focus:ring-sky-500"

    def apply_mixin(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': f'{self.default_classes} w-full',
                    "placeholder": f"Enter {field.label}",
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} w-full",
                    'rows': 3,
                    'style': 'resize: none',
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} mx-2",
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} w-full",
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class': f'{self.default_classes} w-full',
                    "placeholder": f"Enter {field.label}",
                })
                


class Create_Model_Event( For_Mixin, forms.ModelForm ):
    class Meta:
        model = Event
        exclude = ['category']

        widgets = {
            'description': forms.Textarea(attrs={
                "placeholder": "Enter Valid Description about Event:",
            }),

            'date': forms.SelectDateWidget(years=range(2019, 2040)),

            'time': forms.TimeInput(attrs={
                'type': 'time',
            }),

            'location': forms.Textarea(attrs={
                "placeholder": "Enter Valid location",
            }),

            'image': forms.ClearableFileInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_mixin()



class Create_Model_Category( For_Mixin, forms.ModelForm ):
    class Meta:
        model = Category
        fields = '__all__'

        widgets = {
            'description': forms.Textarea(attrs={
                "placeholder": "Enter Valid Description about Category:",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_mixin()



class Create_Model_User( For_Mixin, forms.ModelForm ):
    class Meta:
        model = Participant
        exclude = ['event']

        widget = {
            'email': forms.EmailInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_mixin() 
