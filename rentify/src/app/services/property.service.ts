import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Property } from '../models/property';

@Injectable({
  providedIn: 'root'
})
export class PropertyService {

  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  getProperties(): Observable<{ properties: Property[] }> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Assuming you store the token in localStorage
      })
    };
    console.log(httpOptions);
    return this.http.get<{ properties: Property[] }>(`${this.apiUrl}/properties`, httpOptions);
  }

  getProperty(id: string): Observable<Property> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Assuming you store the token in localStorage
      })
    };
    return this.http.get<Property>(`${this.apiUrl}/property/${id}`, httpOptions);
  }

  createProperty(property: Property): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Assuming you store the token in localStorage
      })
    };
    return this.http.post(`${this.apiUrl}/properties`, property, httpOptions);
  }
  
  deleteProperty(id: string): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Assuming you store the token in localStorage
      })
    };
    return this.http.delete<any>(`${this.apiUrl}/property/${id}`, httpOptions);
  }
  
  likeProperty(id: string): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Assuming you store the token in localStorage
      })
    };
    return this.http.post<any>(`${this.apiUrl}/property/${id}/like`, {}, httpOptions);
  }

  expressInterest(id: string): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      })
    };
    return this.http.post<any>(`${this.apiUrl}/property/${id}/interest`, {}, httpOptions);
  }
}
