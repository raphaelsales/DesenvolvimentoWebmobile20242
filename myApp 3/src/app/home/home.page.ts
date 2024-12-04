import { Component } from '@angular/core';
import { NavController } from '@ionic/angular';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  movies: any[] = [];

  constructor(
    private http: HttpClient,
    private navCtrl: NavController
  ) {
    this.loadMovies();
  }

  loadMovies() {
    this.http.get(`${environment.apiUrl}/api/home/`, { withCredentials: true }).subscribe((data: any) => {
      this.movies = data.movies;
    });
  }

  refresh(event: any) {
    this.loadMovies();
    event.target.complete();
  }

  openMovieDetails(movieId: number) {
    this.navCtrl.navigateForward(`/movie-details/${movieId}`);
  }

  goToProfile() {
    if (this.isAuthenticated()) {
      this.navCtrl.navigateForward('/profile');
    } else {
      this.navCtrl.navigateForward('/login');
    }
  }

  isAuthenticated(): boolean {
    return document.cookie.includes('sessionid');
  }
}
