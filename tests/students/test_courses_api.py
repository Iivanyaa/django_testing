# tests/test_courses.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    course = course_factory()
    url = reverse('course-detail', args=[course.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == course.id

@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    courses = course_factory(_quantity=3)
    url = reverse('course-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 3

@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    course = course_factory()
    url = reverse('course-list') + f'?id={course.id}'
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == course.id

@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    course = course_factory(name='Test Course')
    url = reverse('course-list') + f'?name={course.name}'
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == course.name

@pytest.mark.django_db
def test_create_course(api_client):
    data = {'name': 'New Course'}
    url = reverse('course-list')
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['name'] == data['name']

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course = course_factory()
    data = {'name': 'Updated Course'}
    url = reverse('course-detail', args=[course.id])
    response = api_client.put(url, data, format='json')
    assert response.status_code == 200
    assert response.data['name'] == data['name']

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory()
    url = reverse('course-detail', args=[course.id])
    response = api_client.delete(url)
    assert response.status_code == 204
