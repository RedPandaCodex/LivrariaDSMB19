import { Injectable, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { Autor } from "../models/autor";
import { environments } from "../environments/environments"; 

@Injectable({providedIn: 'root'})
export class AutorService{
    private http = inject(HttpClient)
    private base = environments.apibase
    listar(): Observable<Autor[]>{
        const url = `${this.base}/api/autores/`;
        return this.http.get<Autor[]>(url)
    }
}