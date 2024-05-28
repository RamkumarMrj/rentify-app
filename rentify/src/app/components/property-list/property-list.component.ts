import { Component, OnInit } from '@angular/core';
import { PropertyService } from '../../services/property.service';
import { Property } from '../../models/property';

@Component({
  selector: 'app-property-list',
  templateUrl: './property-list.component.html',
  styleUrl: './property-list.component.css'
})
export class PropertyListComponent implements OnInit {
  properties: Property[] = [];

  constructor(private propertyService: PropertyService) { }

  ngOnInit(): void {
    this.propertyService.getProperties().subscribe((data:any) => {
      this.properties = data;
    });
  }

  onLike(id: string | undefined): void {
    if (id) {
      this.propertyService.likeProperty(id).subscribe(() => {
        const property = this.properties.find(p => p.id === id);
        if (property) {
          property.likes = (property.likes || 0) + 1;
        }
      });
    }
  }

  onInterested(id: string): void {
    this.propertyService.expressInterest(id).subscribe(() => {
      // Handle interest success
    });
  }

  onDelete(id: string): void {
    if (id) {
      this.propertyService.deleteProperty(id).subscribe(() => {
        this.properties = this.properties.filter(property => property.id !== id);
      });
    }
  }
}
