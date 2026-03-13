import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { RegisterComponent } from './register/register.component';
import { RecruiterComponent } from './recruiter/recruiter.component';
import { RecruiterDetailsComponent } from './recruiter-details/recruiter-details.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { ProfileComponent } from './profile/profile.component';
import { ScheduleInterviewComponent } from './schedule-interview/schedule-interview.component';
import { AiAssistantComponent } from './ai-assistant/ai-assistant.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'recruiter', component: RecruiterComponent },
  { path: 'recruiter-details', component: RecruiterDetailsComponent },
  { path: 'forgot-password', component: ForgotPasswordComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'schedule-interview', component: ScheduleInterviewComponent },
  { path: 'ai-assistant', component: AiAssistantComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
