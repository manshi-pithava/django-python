from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages  # Import Django messages framework
from django.contrib.auth.decorators import login_required

from admin_panel.models import Product

from admin_panel.models import Feedback


def index(request):
    storage = messages.get_messages(request)
    storage.used = True  # ✅ This clears any lingering messages from session
    products = Product.objects.all()
    return render(request, "core_templates/index.html", {"products": products})

def base(request):
    return render(request, 'core_templates/base.html')

def about(request):
    return render(request, 'core_templates/about.html')


login_required(login_url="login")   # Only logged-in users can contact
def contact_view(request):
    user = request.user  # Get the logged-in user

    if request.method == "POST":
        name = user.username  # Get full name
        user_email = user.email  # User's email
        message = request.POST.get("message")  # Only message is entered

        # Construct email content
        full_message = f"Name: {name}\nEmail: {user_email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject="New Contact Form Submission",
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,

            )
            messages.success(request, "Your message has been sent successfully!")
        except BadHeaderError:
            messages.error(request, "Invalid header found.")
        except Exception as e:
            messages.error(request, f"Something went wrong: {str(e)}")

        return redirect("contact")

    return render(request, "core_templates/contact.html", {"user": user})  # Pass user to template


def submit_feedback(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        Feedback.objects.create(name=name, email=email, message=message)
        messages.success(request, "Thank you for your feedback!")
        return redirect('submit_feedback')

    return render(request, 'core_templates/user_feedback.html')