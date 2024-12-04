import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { NavController, ToastController } from '@ionic/angular';

@Component({
  selector: 'app-register',
  templateUrl: 'register.page.html',
  styleUrls: ['register.page.scss'],
})
export class RegisterPage {
  usuario: string = '';
  email: string = '';
  senha: string = '';

  constructor(
    private http: HttpClient,
    private navCtrl: NavController,
    private toastController: ToastController
  ) {}

  getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || null;
    return null;
  }

  async onRegister(event: Event) {
    event.preventDefault();
    const csrfToken = this.getCookie('csrftoken');
    this.http.post(`${environment.apiUrl}/api/register/`, { usuario: this.usuario, email: this.email, senha: this.senha }, {
      headers: {
        'X-CSRFToken': csrfToken || ''
      },
      withCredentials: true
    }).subscribe(
      async (response: any) => {
        const toast = await this.toastController.create({
          message: 'Cadastro realizado com sucesso!',
          duration: 2000,
          color: 'success',
        });
        await toast.present();
        this.navCtrl.navigateRoot('/login');
      },
      async (error: any) => {
        const toast = await this.toastController.create({
          message: 'Erro no cadastro. Tente novamente.',
          duration: 2000,
          color: 'danger',
        });
        await toast.present();
      }
    );
  }
}