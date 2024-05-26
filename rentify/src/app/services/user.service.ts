import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { User } from '../models/user';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  register(user: User): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, user);
  }

  login(credentials: {email: string, password: string, user_type: string}): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, credentials);
  }

  getUserDetails(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/user/details`);
  }
}
