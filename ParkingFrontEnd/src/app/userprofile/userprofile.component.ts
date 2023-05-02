import { Component } from '@angular/core';
import { HTTPServiceService } from '../httpservice.service';
import { Router } from 'express';
import {Observable} from 'rxjs';
import { user } from '../user';

@Component({
  selector: 'app-userprofile',
  templateUrl: './userprofile.component.html',
  styleUrls: ['./userprofile.component.css']
})
export class UserprofileComponent {
  users: Observable<user[]>
  constructor(private httpService:HTTPServiceService, private router: Router){

  }

  onDelete(_id:string){
    this.httpService.deleteUser(_id).subscribe(
      data=>{
        console.log(data);
        this.onReload();
      },
      error => console.log(error)
    )
    this.onReload();
  }

  onUpdate(){
    
  }

  onReload(){
    this.users = this.httpService.getUserList();
  }


}
