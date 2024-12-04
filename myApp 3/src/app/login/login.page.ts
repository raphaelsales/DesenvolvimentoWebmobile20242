import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { NavController, ToastController } from '@ionic/angular';

@Component({
  selector: 'app-login',
  templateUrl: 'login.page.html',
  styleUrls: ['login.page.scss'],
})
export class LoginPage {
  usuario: string = '';
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

  async onLogin(event: Event) {
    event.preventDefault();
    const csrfToken = this.getCookie('csrftoken');
    this.http.post(`${environment.apiUrl}/api/login/`, { usuario: this.usuario, senha: this.senha }, {
      headers: {
        'X-CSRFToken': csrfToken || ''
      },
      withCredentials: true
    }).subscribe(
      async (response: any) => {
        const toast = await this.toastController.create({
          message: 'Login realizado com sucesso!',
          duration: 2000,
          color: 'success',
        });
        await toast.present();
        this.navCtrl.navigateRoot('/');
      },
      async (error: any) => {
        const toast = await this.toastController.create({
          message: 'Erro no login. Usuário ou senha inválidos.',
          duration: 2000,
          color: 'danger',
        });
        await toast.present();
      }
    );
  }
}