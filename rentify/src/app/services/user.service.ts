import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Inject, Injectable, PLATFORM_ID } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { User } from '../models/user';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  // private apiUrl = 'http://localhost:5000/api';
  private apiUrl = 'http://ec2-13-201-67-46.ap-south-1.compute.amazonaws.com:5000/api'

  constructor(private http: HttpClient,private router: Router, @Inject(PLATFORM_ID) private platformId: Object) { }

  register(user: User): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, user);
  }

  login(credentials: {email: string, password: string, user_type: string}): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, credentials);
  }

  getUserDetails(): Observable<User> {
    let token: string | null = null;
    if (isPlatformBrowser(this.platformId)) {
      token = localStorage.getItem('access_token');
    }

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
