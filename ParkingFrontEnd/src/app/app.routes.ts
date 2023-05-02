import { Route, Routes } from "@angular/router";

import { HomepageComponent } from "./homepage/homepage.component";
import { LoginComponent } from "./login/login.component";
import { SignupComponent } from "./signup/signup.component";
import { ViewLotsComponent } from "./view-lots/view-lots.component";
import { UserprofileComponent } from "./userprofile/userprofile.component";

export const appRoutes: Routes = [
    {path: 'home', component:HomepageComponent},
    {path:'login', component:LoginComponent},
    {path:'register',component:SignupComponent},
    {path:'view-lots',component:ViewLotsComponent},
    {path:'user',component:UserprofileComponent},
    {path:'',redirectTo:'home',pathMatch:'full'}
]