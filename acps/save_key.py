def handle_uploaded_file(f, username):
    with open("acps/keys/" + username + ".key", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
