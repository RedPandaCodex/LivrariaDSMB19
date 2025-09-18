import { CanActivateFn, Route } from "@angular/router";
import { inject } from "@angular/core";
import { AuthService } from "../services/auth.service";
import { Router } from "express";

export const authGuard: CanActivateFn = ()=>{
    const auth = inject(AuthService)
    const router = inject(Router)

    if (auth.isAuthenticaded()) return true;
    
    router.navigateByUrl('/login')

    return false
}