import { Component } from '@angular/core';
import { Property } from '../../models/property';
import { PropertyService } from '../../services/property.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-property-create',
  templateUrl: './property-create.component.html',
  styleUrl: './property-create.component.css'
})
export class PropertyCreateComponent {
  property: Property = {
    place: '',
    area: "",
    price: 0,
    bedrooms: 0,
    bathrooms: 0,
    amenities: [],
    description: '',
    image: ''
  };

  constructor(private propertyService: PropertyService, private router: Router) {}

  createProperty(): void {
    this.propertyService.createProperty(this.property).subscribe(() => {
      this.router.navigate(['/properties']);
    });
  }

}
