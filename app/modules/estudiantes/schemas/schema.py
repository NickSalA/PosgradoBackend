"""Esquemas para el módulo de estudiantes"""
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.modules.estudiantes.models.student import StatusStudent, TypeDocumentStudent
from app.modules.estudiantes.models.program_student import StatusStudentProgram

class PersonBase(BaseModel):
    name: str = Field(...,min_length=2, max_length=100)
    paternal_surname: str = Field(..., min_length=2, max_length=100)
    maternal_surname: str = Field(..., min_length=2, max_length=100)
    status: StatusStudent = Field(default=StatusStudent.ACTIVE)

    # Campos opcionales
    identity_document: str | None= Field(default=None, max_length=20)
    type_document: TypeDocumentStudent | None = Field(default=None)
    nationality: str | None = Field(default=None, max_length=100)
    phone: str | None = Field(default=None, max_length=15)
    academic_email: EmailStr | None = Field(default=None, max_length=100)
    personal_email: EmailStr | None = Field(default=None, max_length=100)

class PersonInfo(PersonBase):
    model_config = ConfigDict(from_attributes=True)

class AcademicCommon(BaseModel):
    code: str = Field(..., min_length=8, max_length=8)
    status: StatusStudentProgram = Field(default=StatusStudentProgram.ACTIVE)

    # Campos opcionales
    curriculum: int | None = Field(default=None)
    admission_year: int | None = Field(default=None)
    graduation_year: int | None = Field(default=None)

class AcademicBase(AcademicCommon):
    program_id: int = Field(...)

class ProgramInfo(BaseModel):
    id: int
    name: str
    degree: str
    mention: str | None = None

    model_config = ConfigDict(from_attributes=True)

class AcademicInfo(AcademicCommon):
    program: ProgramInfo

    model_config = ConfigDict(from_attributes=True)

class StudentCreate(BaseModel):
    person: PersonBase
    academic: AcademicBase

class StudentUpdate(BaseModel):
    phone: str | None = None
    personal_email: EmailStr | None = None
    academic_email: EmailStr | None = None
    nationality: str | None = None
    type_document: str | None = None
    identity_document: str | None = None
    status_personal: StatusStudent | None = None

    # Academico
    curriculum: int | None = None
    graduation_year: int | None = None
    status_academic: StatusStudentProgram | None = None


# RESPONSES
class StudentManagement(BaseModel):
    id: int
    code: str
    type_document: str | None
    identity_document: str | None
    name: str
    paternal_surname: str
    maternal_surname: str
    program_name: str
    degree: str
    mention: str | None = None
    status: StatusStudentProgram

    model_config = ConfigDict(from_attributes=True)

class StudentDashboard(BaseModel):
    """Esquema para el dashboard del estudiante"""
    id: int
    personal: PersonInfo
    academic: AcademicInfo

    model_config = ConfigDict(from_attributes=True)
