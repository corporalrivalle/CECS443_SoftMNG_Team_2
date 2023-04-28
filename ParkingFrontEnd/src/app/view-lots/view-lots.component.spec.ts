import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewLotsComponent } from './view-lots.component';

describe('ViewLotsComponent', () => {
  let component: ViewLotsComponent;
  let fixture: ComponentFixture<ViewLotsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ViewLotsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewLotsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
