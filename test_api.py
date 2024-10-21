import requests

BASE_URL = "https://grade-system-f34a1ea47705.herokuapp.com"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsImZpcnN0bmFtZSI6ImFkbWluIiwibGFzdG5hbWUiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImFjYWRlbWljIjp7ImFjYWRlbWljX2lkIjoxLCJhY2FkZW1pY19uYW1lIjoi4Lin4Li04Lio4Lin4LiB4Lij4Lij4Lih4LiL4Lit4Lif4LiV4LmM4LmB4Lin4Lij4LmMIn0sImlhdCI6MTcyOTQ5OTY0NywiZXhwIjoxNzI5NTAzMjQ3fQ.9DkbaVm8y5jr77JHtTynvvssWPsns1jUPzyuw2SJAgY"

teacher_id = None  # กำหนดตัวแปร global สำหรับ teacher_id
TITLENAME = "Dr."
FIRSTNAME = "หดหกกก้้้ดดดกเห"
LASTNAME = "หกดหหเ้่เกดกดเก"

def test_create_Teacher():
    global teacher_id  # ใช้ตัวแปร global
    # เพิ่ม headers สำหรับการรับรองความถูกต้อง
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    
    response = requests.post(f"{BASE_URL}/api/createTeacher",
                             json={'titlename': TITLENAME, 'firstname': FIRSTNAME, 'lastname': LASTNAME},
                             headers=headers)
    
    print("Response Code:", response.status_code)
    print("Response Text:", response.text)  # ดูข้อความตอบกลับ
    
    assert response.status_code == 201
    response_data = response.json()
    
    assert 'teacher_id' in response_data
    teacher_id = response_data['teacher_id'] # เก็บ teacher_id
    assert response_data['titlename'] == TITLENAME
    assert response_data['firstname'] == FIRSTNAME
    assert response_data['lastname'] == LASTNAME

def test_get_teachers():
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    
    # Get the list of teachers
    response = requests.get(f"{BASE_URL}/api/getTeachers", headers=headers)
    
    print("Response Code:", response.status_code)
    print("Response Text:", response.text)  # ดูข้อความตอบกลับ
    
    assert response.status_code == 200
    response_data = response.json()
    
    assert isinstance(response_data, list)  # ตรวจสอบว่า response_data เป็นรายการ
    assert len(response_data) > 0  # ตรวจสอบว่ามีครูในรายการ
    for teacher in response_data:
        assert 'teacher_id' in teacher
        assert 'titlename' in teacher
        assert 'firstname' in teacher
        assert 'lastname' in teacher
        # ตรวจสอบข้อมูลที่คาดหวัง เช่น
        assert isinstance(teacher['teacher_id'], int)
        assert isinstance(teacher['titlename'], str)
        assert isinstance(teacher['firstname'], str)
        assert isinstance(teacher['lastname'], str)

def test_delete_teacher():
    global teacher_id  # ใช้ตัวแปร global
    headers = {
        'Authorization': f'Bearer {TOKEN}'
    }
    response = requests.get(f"{BASE_URL}/api/getTeacher/{teacher_id}", headers=headers)
    print("Get Teacher Response Code:", response.status_code)
    print("Get Teacher Response Text:", response.text)
    # ตรวจสอบว่ามี teacher_id ที่สร้างขึ้นมาก่อน
    assert teacher_id is not None, "No teacher_id available for deletion"
    
    # Delete the created teacher
    response = requests.delete(f"{BASE_URL}/api/deleteTeacher/{teacher_id}", headers=headers)
    
    print("Delete Response Code:", response.status_code)
    print("Delete Response Text:", response.text)  # ดูข้อความตอบกลับ
    
    assert response.status_code == 204, f"Failed to delete teacher: {response.text}"

    # Try to get the deleted teacher
    response = requests.get(f"{BASE_URL}/api/getTeacher/{teacher_id}", headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == 'Teacher not found'