from course.models import Articles, Categories
from main.models import AboutUser


def check_user(article, user, is_superuser):
    if is_superuser:
        return True
    
    userInfo = AboutUser.objects.get(user=user)
    userCoursesSet = set([elem for elem in userInfo.passed_courses.all()])
    neededCourses = set([elem for elem in article.required.all()])
    return neededCourses.issubset(userCoursesSet)

