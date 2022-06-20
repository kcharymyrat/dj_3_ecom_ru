from django import template
from django.utils.safestring import mark_safe

register = template.Library()

TABLE_HEAD = """
<table>
    <tbody>
"""

TABLE_TAIL = """
    </tbody>
</table
"""


TABLE_CONTENT = """
<tr>
    <td>{name}</td>
    <td>{value}</td>    
</tr>
"""

PRODUCT_SPEC = {
    "notebook": {
        "Diagonal": "diagonal",
        "Displaye type": "display_type",
        "Processor frequency": "processor_freq",
        "RAM": "ram",
        "Video": "video",
        "Battery standby": "time_without_charge",
    },
    "smartphone": {
        "Diagonal": "diagonal",
        "Displaye type": "display_type",
        "Resolution": "resolution",
        "Accumulator": "accum_volume",
        "RAM": "ram",
        "SD": "sd",
        "Max SD Volume": "sd_volume_max",
        "Main Camera (MPx)": "main_cam_mp",
        "Frontal Camera (MPx)": "frontal_cam_mp",
    },
}


def get_product_spec(product, model_name):
    table_content = ""
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
