import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HTTPServiceService {
  private baseUrl = 'http://localhost:5000/'
  constructor(private http: HttpClient) { }

  createUser(user:Object):Observable<Object>{
    return this.http.post(`${this.baseUrl}`,user)
  }

  deleteUser(_id:string):Observable<Object>{
    return this.http.delete(`${this.baseUrl}/${_id}`,{responseType:'text'})
  }

  getUserList(): Observable<any> {
    return this.http.get(`${this.baseUrl}`);
  }
}
