import { Component } from '@angular/core';
import { HTTPServiceService } from '../httpservice.service';
import { Router } from '@angular/router';
import { map } from 'rxjs/operators';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-view-lots',
  templateUrl: './view-lots.component.html',
  styleUrls: ['./view-lots.component.css']
})
export class ViewLotsComponent {
  lotList;
  constructor(private httpService: HTTPServiceService, private router: Router){}

  onReload(){
    console.log("Reload triggered")
    this.httpService.getLotData().pipe(map(data => this.lotList = data)).subscribe();
  }

}
