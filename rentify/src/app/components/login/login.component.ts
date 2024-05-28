import { Component } from '@angular/core';
import { UserService } from '../../services/user.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  email: string = '';
  password: string = '';
  user_type: string = '';

  constructor(private userService: UserService, private router: Router) {}

  login() {
    this.userService.login({ email: this.email, password: this.password, user_type: this.user_type }).subscribe(
      (response) => {
        localStorage.setItem('access_token', response.access_token);
        this.router.navigate(['/user']);
      },
      (error) => {
        console.error('Login failed', error);
      }
    );
  }
}
