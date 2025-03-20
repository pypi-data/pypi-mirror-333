from fastapi import Depends, HTTPException

from rb_commons.configs.injections import get_claims
from rb_commons.schemes.jwt import Claims, UserRole


class BasePermission:
    def __call__(self, claims: Claims = Depends(get_claims)):
        if not self.has_permission(claims):
            raise HTTPException(status_code=403, detail="Permission Denied")

    def has_permission(self, claims: Claims) -> bool:
        return False


class IsAdmin(BasePermission):
    def has_permission(self, claims: Claims) -> bool:
        return claims.user_role == UserRole.ADMIN


class IsCustomer(BasePermission):
    def has_permission(self, claims: Claims) -> bool:
        return claims.user_role == UserRole.CUSTOMER
