from django.shortcuts import render
from django.http import  Http404
def tool_list(request):
    tools = [
        {
        "name": "FTK Imager",
        "desc": "Disk imajı alma ve delil koruma aracı.",
        "slug": "ftk-imager",
        "image": "images/FTK.png"
        },
        {
        "name": "Autopsy",
        "desc": "Açık kaynak dijital adli analiz platformu.",
        "slug": "autopsy",
        "image": "images/autopsy.jpg"
        },
        {
        "name": "Wireshark",
        "desc": "Ağ trafiğini analiz etmek için kullanılan güçlü bir araç.",
        "slug": "wireshark",
        "image": "images/wireshark.png"
        },
        {
        "name": "Volatility",
        "desc": "RAM bellek analizleri için kullanılır.",
        "slug": "volatility",
        "image": "images/vovality.jpeg"
        },
    ]
    return render(request, 'forensic_lab/tool_list.html', {"tools": tools})
def tool_detail(request, slug):
    valid_slugs = ["ftk-imager", "autopsy", "wireshark", "volatility"]
    if slug not in valid_slugs:
        raise Http404("Araç Bulunamadı")

    # slug'ı template adına dönüştür
    template_name = f"forensic_lab/{slug.replace('-', '_')}.html"
    return render(request, template_name)
