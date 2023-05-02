import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'ParkingFrontEnd';

  constructor(private router: Router){}

  homeRedirect(){
    this.router.navigate(['home']);
  }

  registerRedirect(){
    this.router.navigate(['register']);
  }

  lotsRedirect(){
    this.router.navigate(['view-lots']);
  }

  userRedirect(){
    this.router.navigate(['user'])
  }


}
