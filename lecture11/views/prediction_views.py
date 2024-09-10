def prediction(request):
    if request.method == "POST":
        controller = PredictionController(request)
        response = controller.reponse
    return template_render("predict.html",context={response})

