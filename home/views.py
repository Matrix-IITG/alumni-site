import urllib3

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User

from alumni.forms import ProfileForm
from alumni.models import Alumni
from .forms import UserForm

from lxml import html
import csv, os, json
import requests
from django.utils import timezone
#from selenium import webdriver
import bs4 as bs
import urllib3
# Create your views here.
def home(request):
    return render(request,'home/index.html')
def about_us(request):
    return render(request,'home/about.html')
def team(request):
    return render(request,'home/team.html')

########### views for user accounts
def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        name = form.cleaned_data["name"]
        ln_link = form.cleaned_data["ln_link"]
        fb_link = form.cleaned_data["fb_link"]
        curr_work = form.cleaned_data["curr_work"]
        pre_work = form.cleaned_data["pre_work"]
        group=form.cleaned_data['group']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        my_group = Group.objects.get(name=group)
        new_Alumni=Alumni.objects.create(user=user,name=name,roll_no=username,ln_link=ln_link,fb_link=fb_link,curr_work = curr_work,prev_work=pre_work)
        new_Alumni.save()
        my_group.user_set.add(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'home/index.html')
    context = {
        "form": form,
    }
    return render(request, 'registration/register.html', context)

@login_required
@permission_required('polls.can_vote')
def update_user(request):
    alumni=Alumni.objects.all()
    cur_year=(timezone.now().year)/100
    for user1 in alumni:
        admi_date = (user1.roll_no) / 10000000
        user = get_object_or_404(User, username=str(user1.roll_no))
        if cur_year - admi_date <= 4:
            remove_group = Group.objects.get(name='Alumni')
            remove_group.user_set.remove(user)
            add_group = Group.objects.get(name='Students')
            add_group.user_set.add(user)
        else:
            remove_group = Group.objects.get(name='Students')
            remove_group.user_set.remove(user)
            add_group = Group.objects.get(name='Alumni')
            add_group.user_set.add(user)
    return render(request,'registration/user_updates.html',{'alumni':alumni,})

@login_required
def profile(request):
    alumni = Alumni.objects.filter(user=request.user)
    return render(request,'registration/profile.html',{'alumni':alumni})
@login_required
def profile_edit_manual(request):
    # # driver = webdriver.Firefox(executable_path=r'your\path\geckodriver.exe')  # I actually used the chromedriver and did not test firefox, but it should work.
    # # profile_link = "https://www.linkedin.com/in/ashish-ranjan-753429136/"
    # # driver.get(profile_link)
    # # html = driver.page_source
    # # soup = bs.BeautifulSoup(html,'lxml')  # specify parser or it will auto-select for you
    # # summary = soup.find('section', {"id": "summary"})
    # # print (summary.getText())
    urlopener = urllib3.build_opener()
    urlopener.addheaders = [('User-agent', 'Mozilla/5.0')]
    sauce = urlopener.open('https://www.linkedin.com/in/deepakgouda/').read()
    #sauce = urllib3.urlopen('https://www.linkedin.com/in/ashish-ranjan-753429136/').read()
    soup=bs.BeautifulSoup(sauce,'lxml')
    print(soup)
    alumni=get_object_or_404(Alumni, user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST,instance=alumni)
        if form.is_valid():
            alumni = form.save(commit=False)
            alumni.save()
            return redirect('home:profile')
    else:
        form = ProfileForm()
    return render(request, 'registration/edit_profile.html', {'form': form,})
def profile_edit_linkdin(request):
    # # driver = webdriver.Firefox(executable_path=r'your\path\geckodriver.exe')  # I actually used the chromedriver and did not test firefox, but it should work.
    # # profile_link = "https://www.linkedin.com/in/ashish-ranjan-753429136/"
    # # driver.get(profile_link)
    # # html = driver.page_source
    # # soup = bs.BeautifulSoup(html,'lxml')  # specify parser or it will auto-select for you
    # # summary = soup.find('section', {"id": "summary"})
    # # print (summary.getText())
    urlopener = urllib3.build_opener()
    urlopener.addheaders = [('User-agent', 'Mozilla/5.0')]
    sauce = urlopener.open('https://www.linkedin.com/in/aditya-mittal-709a1162/').read()
    #sauce = urllib3.urlopen('https://www.linkedin.com/in/ashish-ranjan-753429136/').read()
    soup=bs.BeautifulSoup(sauce,'lxml')
    tag1=soup.findAll('ul')
    #data=soup.findAll('section' ,attrs={'class':'profile-section','id':'topcard'})
    # for x in soup.findAll('section' ,attrs={'class':'profile-section','id':'topcard'}):
    #     print(x)
    #data = soup.find('section', attrs={'class': 'profile-section', 'id': 'topcard'})
    name= soup.find('section' ,attrs={'class':'profile-section','id':'topcard'}).find('h1',attrs={'class':'fn'})
    final_name=name.text
    location = soup.find('section', attrs={'class': 'profile-section', 'id': 'topcard'}).find('span', attrs={'class': 'locality'})
    final_location=location.text
    skills_soup=soup.find('section', attrs={'class': 'profile-section', 'id': 'skills'}).find_all('li')
    skills=[""]*len(skills_soup)
    i=0
    for li in skills_soup:
        skills[i]=skills_soup[i].text
        i=i+1
    final_skills=skills[:len(skills_soup)-3]
    #id=data.findAll('section' ,attrs={'id':'topcard'})
    #print(soup.prettify())
    #print(soup.title)
    #print(vol)
    #print(skills[:len(vol)-3])
    #for ski in skills:
    #    print(ski)
    print(final_name)
    print(final_location)
    print(final_skills)
    alumni=get_object_or_404(Alumni, user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST,instance=alumni)
        if form.is_valid():
            alumni = form.save(commit=False)
            alumni.save()
            return redirect('home:profile')
    else:
        form = ProfileForm()
    return render(request, 'registration/edit_profile.html', {'form': form,})

################## parsers
def linkedin_companies_parser(url):
    url="https: // www.linkedin.com / in / ashish - ranjan - 753429136 /"
    for i in range(5):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'
            }
            print ("Fetching :", url)
            response = requests.get(url, headers=headers, verify=False)
            formatted_response = response.content.replace('<!--', '').replace('-->', '')
            doc = html.fromstring(formatted_response)
            datafrom_xpath = doc.xpath('//code[@id="stream-promo-top-bar-embed-id-content"]//text()')
            content_about = doc.xpath('//code[@id="stream-about-section-embed-id-content"]')
            if not content_about:
                content_about = doc.xpath('//code[@id="stream-footer-embed-id-content"]')
            if content_about:
                pass
                # json_text = content_about[0].html_content().replace('<code id="stream-footer-embed-id-content"><!--','').replace('<code id="stream-about-section-embed-id-content"><!--','').replace('--></code>','')

            if datafrom_xpath:
                try:
                    json_formatted_data = json.loads(datafrom_xpath[0])
                    company_name = json_formatted_data[
                        'companyName'] if 'companyName' in json_formatted_data.keys() else None
                    size = json_formatted_data['size'] if 'size' in json_formatted_data.keys() else None
                    industry = json_formatted_data['industry'] if 'industry' in json_formatted_data.keys() else None
                    description = json_formatted_data[
                        'description'] if 'description' in json_formatted_data.keys() else None
                    follower_count = json_formatted_data[
                        'followerCount'] if 'followerCount' in json_formatted_data.keys() else None
                    year_founded = json_formatted_data[
                        'yearFounded'] if 'yearFounded' in json_formatted_data.keys() else None
                    website = json_formatted_data['website'] if 'website' in json_formatted_data.keys() else None
                    type = json_formatted_data['companyType'] if 'companyType' in json_formatted_data.keys() else None
                    specialities = json_formatted_data[
                        'specialties'] if 'specialties' in json_formatted_data.keys() else None

                    if "headquarters" in json_formatted_data.keys():
                        city = json_formatted_data["headquarters"]['city'] if 'city' in json_formatted_data[
                            "headquarters"].keys() else None
                        country = json_formatted_data["headquarters"]['country'] if 'country' in json_formatted_data[
                            'headquarters'].keys() else None
                        state = json_formatted_data["headquarters"]['state'] if 'state' in json_formatted_data[
                            'headquarters'].keys() else None
                        street1 = json_formatted_data["headquarters"]['street1'] if 'street1' in json_formatted_data[
                            'headquarters'].keys() else None
                        street2 = json_formatted_data["headquarters"]['street2'] if 'street2' in json_formatted_data[
                            'headquarters'].keys() else None
                        zip = json_formatted_data["headquarters"]['zip'] if 'zip' in json_formatted_data[
                            'headquarters'].keys() else None
                        street = street1 + ', ' + street2
                        print(street)
                    else:
                        city = None
                        country = None
                        state = None
                        street1 = None
                        street2 = None
                        street = None
                        zip = None

                    data = {
                        'company_name': company_name,
                        'size': size,
                        'industry': industry,
                        'description': description,
                        'follower_count': follower_count,
                        'founded': year_founded,
                        'website': website,
                        'type': type,
                        'specialities': specialities,
                        'city': city,
                        'country': country,
                        'state': state,
                        'street': street,
                        'zip': zip,
                        'url': url
                    }
                    return data
                except:
                    print ("cant parse page", url)

            # Retry in case of captcha or login page redirection
            if len(response.content) < 2000 or "trk=login_reg_redirect" in url:
                if response.status_code == 404:
                    print ("linkedin page not found")
                else:
                    raise Exception('redirecting to login page or captcha found')
        except:
            print ("retrying :", url)


def readurls():
    companyurls = ['https://www.linkedin.com/company/tata-consultancy-services']
    extracted_data = []
    for url in companyurls:
        extracted_data.append(linkedin_companies_parser(url))
        f = open('data.json', 'w')
        json.dump(extracted_data, f, indent=4)


if __name__ == "__main__":
    readurls()
