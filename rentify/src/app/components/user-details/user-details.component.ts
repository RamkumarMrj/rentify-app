import { Component, OnInit } from '@angular/core';
import { UserService } from '../../services/user.service';
import { User } from '../../models/user';

@Component({
  selector: 'app-user-details',
  templateUrl: './user-details.component.html',
  styleUrl: './user-details.component.css'
})
export class UserDetailsComponent implements OnInit {
  user: User | null = null;

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.userService.getUserDetails().subscribe({
      next: (user) => this.user = user,
      error: (err) => console.error('Failed to load user details', err)
    });
  }
}
