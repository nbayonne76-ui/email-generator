from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Partner
from app.schemas import PartnerCreate, PartnerRead, PartnerUpdate

router = APIRouter(prefix="/partners", tags=["partners"])


def _get_or_404(db: Session, partner_id: int) -> Partner:
    partner = db.get(Partner, partner_id)
    if partner is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Partenaire introuvable")
    return partner


def _commit_or_409(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Un partenaire avec cet email existe déjà"
        ) from None


def _to_columns(data: dict) -> dict:
    if "metadata" in data:
        data["metadata_"] = data.pop("metadata")
    return data


@router.get("", response_model=list[PartnerRead])
def list_partners(db: Session = Depends(get_db)) -> list[Partner]:
    return list(db.scalars(select(Partner).order_by(Partner.name)))


@router.get("/{partner_id}", response_model=PartnerRead)
def get_partner(partner_id: int, db: Session = Depends(get_db)) -> Partner:
    return _get_or_404(db, partner_id)


@router.post("", response_model=PartnerRead, status_code=status.HTTP_201_CREATED)
def create_partner(payload: PartnerCreate, db: Session = Depends(get_db)) -> Partner:
    partner = Partner(**_to_columns(payload.model_dump()))
    db.add(partner)
    _commit_or_409(db)
    db.refresh(partner)
    return partner


@router.patch("/{partner_id}", response_model=PartnerRead)
def update_partner(
    partner_id: int, payload: PartnerUpdate, db: Session = Depends(get_db)
) -> Partner:
    partner = _get_or_404(db, partner_id)
    for field, value in _to_columns(payload.model_dump(exclude_unset=True)).items():
        setattr(partner, field, value)
    _commit_or_409(db)
    db.refresh(partner)
    return partner


@router.delete("/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_partner(partner_id: int, db: Session = Depends(get_db)) -> Response:
    db.delete(_get_or_404(db, partner_id))
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
