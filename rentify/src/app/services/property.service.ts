import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Property } from '../models/property';

@Injectable({
  providedIn: 'root'
})
export class PropertyService {

  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  createProperty(property: Property): Observable<any> {
    return this.http.post(`${this.apiUrl}/properties`, property);
  }

  getProperties(): Observable<{ properties: Property[] }> {
    return this.http.get<{ properties: Property[] }>(`${this.apiUrl}/properties`);
  }

  getProperty(id: string): Observable<Property> {
    return this.http.get<Property>(`${this.apiUrl}/property/${id}`);
  }

  likeProperty(id: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/property/${id}/like`, {});
  }

  expressInterest(id: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/property/${id}/interest`, {});
  }

  deleteProperty(id: string): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/property/${id}`);
  }

  
}
