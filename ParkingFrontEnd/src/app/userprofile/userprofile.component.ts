import { Component } from '@angular/core';
import { HTTPServiceService } from '../httpservice.service';
import { Router } from '@angular/router';
import {Observable} from 'rxjs';
import { user } from '../user';
import {map, tap, reduce} from 'rxjs/operators';
import { MatTableDataSource, MatTable } from '@angular/material/table';
import {MatPaginator} from '@angular/material/paginator';

@Component({
  selector: 'app-userprofile',
  templateUrl: './userprofile.component.html',
  styleUrls: ['./userprofile.component.css']
})
export class UserprofileComponent {
  users: Observable<user[]>
  userList;
  
  constructor(private httpService:HTTPServiceService, private router: Router){

  }
  
  dataSource = new MatTableDataSource();

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
    console.log(this.userList)
  }


}
