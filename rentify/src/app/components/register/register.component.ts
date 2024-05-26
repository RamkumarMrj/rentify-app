import { Component } from '@angular/core';
import { User } from '../../models/user';
import { UserService } from '../../services/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  user: User = {
    first_name: '',
    last_name: '',
    email: '',
    user_type: '',
    phone_number: ''
  };
  password: string = '';

  constructor(private userService: UserService, private router: Router) {}

  register() {
    const newUser = { ...this.user, password: this.password };
    this.userService.register(newUser).subscribe(() => {
      this.router.navigate(['/login']);
    });
  }
}
