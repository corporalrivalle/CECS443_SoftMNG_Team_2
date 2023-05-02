import { Component } from '@angular/core';
import { HTTPServiceService } from '../httpservice.service';
import { Router } from '@angular/router';
import {map} from 'rxjs/operators';

@Component({
  selector: 'app-userprofile',
  templateUrl: './userprofile.component.html',
  styleUrls: ['./userprofile.component.css']
})
export class UserprofileComponent {
    userList;
  
  constructor(private httpService:HTTPServiceService, private router: Router){

  }
  
  // onDelete(_id:string){
  //   this.httpService.deleteUser(_id).subscribe(
  //     data=>{
  //       console.log(data);
  //       this.onReload();
  //     },
  //     error => console.log(error)
  //   )
  //   this.onReload();
  // }

  // onUpdate(){
    
  // }
  onReload(){
    console.log("Reload triggered")
    this.httpService.getUserList().pipe(map(data => this.userList=data)).subscribe()
  }


}
