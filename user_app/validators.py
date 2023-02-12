from django.core.exceptions import ValidationError
def validate_file_size(value):
    filesize= value.size
    
    if filesize > 2621440:
        raise ValidationError("You cannot upload file more than 2.5Mb")
    else:
        return value