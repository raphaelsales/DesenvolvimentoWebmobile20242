import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { NavController, ToastController } from '@ionic/angular';

@Component({
  selector: 'app-movie-details',
  templateUrl: 'movie-details.page.html',
  styleUrls: ['movie-details.page.scss'],
})
export class MovieDetailsPage implements OnInit {
  movie: any;

  constructor(
    private route: ActivatedRoute,
    private http: HttpClient,
    private navCtrl: NavController,
    private toastController: ToastController
  ) {}

  ngOnInit() {
    const movieId = this.route.snapshot.paramMap.get('movieId') ?? '';
    this.loadMovieDetails(movieId);
  }
  goToProfile() {
    //if (this.isAuthenticated) {
    //  this.navCtrl.navigateForward('/profile');
    //} else {
    //  this.navCtrl.navigateForward('/login');
    //}
    console.log('goToProfile');
  }

  loadMovieDetails(movieId: string | null) {
    this.http.get(`${environment.apiUrl}/api/filme/${movieId}/`).subscribe((data: any) => {
      this.movie = data;
    });
  }

  addToWatchlist() {
    const movieId = this.movie.id;
    this.http.post(`${environment.apiUrl}/api/watchlist/add/`, { movie_id: movieId }).subscribe(
      async (response: any) => {
        const toast = await this.toastController.create({
          message: response.message,
          duration: 2000,
          color: 'success',
        });
        await toast.present();
      },
      async (error: any) => {
        const toast = await this.toastController.create({
          message: 'Erro ao adicionar à lista de desejos.',
          duration: 2000,
          color: 'danger',
        });
        await toast.present();
      }
    );
  }
}