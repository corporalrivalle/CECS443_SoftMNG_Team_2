import { Component } from '@angular/core';
import { FormBuilder, Validators, FormControl, FormGroup} from '@angular/forms'
import { HTTPServiceService } from '../httpservice.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent {
  signUpForm;
  constructor(private formBuilder: FormBuilder, private httpService:HTTPServiceService, private router:Router){
    this.signUpForm = this.formBuilder.group({
      email:['',[Validators.required,Validators.email]],
      username:['',[Validators.required]],
      password:['',[Validators.required]],
      balance:0,
      car_plate:""
    })
  }

  onSubmit(){
    console.log("Generating User!");
    var newUser = {
      "username": this.signUpForm.value.username,
      "email": this.signUpForm.value.email,
      "password":this.signUpForm.value.password,
      "balance": this.signUpForm.value.balance,
      "car_plate":this.signUpForm.value.car_plate
    }
    console.log("Sending Userdata to Database!");
    this.httpService.createUser(newUser).subscribe(
      data=>{
        console.log(data);
      },
      error => console.log(error)
    )
  }

}
