import { Component, OnInit } from '@angular/core';
import { Property } from '../../models/property';
import { ActivatedRoute } from '@angular/router';
import { PropertyService } from '../../services/property.service';

@Component({
  selector: 'app-property-detail',
  templateUrl: './property-detail.component.html',
  styleUrl: './property-detail.component.css'
})
export class PropertyDetailComponent implements OnInit {
  property?: Property;

  constructor(
    private route: ActivatedRoute,
    private propertyService: PropertyService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id')!;
    this.propertyService.getProperty(id).subscribe((data) => {
      this.property = data;
    });
  }

  onLike(): void {
    if (this.property) {
      this.propertyService.likeProperty(this.property.id!).subscribe(() => {
        if (this.property) {
          this.property.likes = (this.property.likes || 0) + 1;
        }
      });
    }
  }

  onInterested(): void {
    if (this.property) {
      this.propertyService.expressInterest(this.property.id!).subscribe(() => {
        // Handle interest success
      });
    }
  }
}
