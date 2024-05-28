import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { User } from '../models/user';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient,private router: Router) { }

  register(user: User): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, user);
  }

  login(credentials: {email: string, password: string, user_type: string}): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, credentials);
  }

  getUserDetails(): Observable<User> {
    const token = localStorage.getItem('access_token');
    console.log('Token from localStorage:', token);

    if (!token) {
      console.error('No token found in localStorage');
      // Handle the case where the token is missing, e.g., redirect to login
      this.router.navigate(['/login']);
      return throwError('Token not found in localStorage');
    }

    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      })
    };
    console.log('HTTP Options:', httpOptions);
    return this.http.get<User>(`${this.apiUrl}/user/details`, httpOptions);
  }
}
