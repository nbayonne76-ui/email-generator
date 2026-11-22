from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Template
from app.schemas import TemplateCreate, TemplateRead, TemplateUpdate

router = APIRouter(prefix="/templates", tags=["templates"])


def _get_or_404(db: Session, template_id: int) -> Template:
    template = db.get(Template, template_id)
    if template is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Template introuvable")
    return template


@router.get("", response_model=list[TemplateRead])
def list_templates(
    category: str | None = None,
    is_active: bool | None = None,
    db: Session = Depends(get_db),
) -> list[Template]:
    stmt = select(Template).order_by(Template.category.nulls_last(), Template.name)
    if category is not None:
        stmt = stmt.where(Template.category == category)
    if is_active is not None:
        stmt = stmt.where(Template.is_active == is_active)
    return list(db.scalars(stmt))


@router.get("/{template_id}", response_model=TemplateRead)
def get_template(template_id: int, db: Session = Depends(get_db)) -> Template:
    return _get_or_404(db, template_id)


@router.post("", response_model=TemplateRead, status_code=status.HTTP_201_CREATED)
def create_template(payload: TemplateCreate, db: Session = Depends(get_db)) -> Template:
    template = Template(**payload.model_dump())
    db.add(template)
    db.commit()
    db.refresh(template)
    return template


@router.patch("/{template_id}", response_model=TemplateRead)
def update_template(
    template_id: int, payload: TemplateUpdate, db: Session = Depends(get_db)
) -> Template:
    template = _get_or_404(db, template_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(template, field, value)
    db.commit()
    db.refresh(template)
    return template


@router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(template_id: int, db: Session = Depends(get_db)) -> Response:
    db.delete(_get_or_404(db, template_id))
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
