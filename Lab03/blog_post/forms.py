from django import forms
from .models import Post,Block

class PostForm(forms.ModelForm):
        def __init__(self, *args, **kwargs):
            super(PostForm, self).__init__(*args, **kwargs)
            for field in self.visible_fields():
                field.field.widget.attrs["class"] = "form-control"

        class Meta:
            model = Post
            exclude=("author","created_on","last_modified")

class BlockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Block
        exclude = ["blocker"]
