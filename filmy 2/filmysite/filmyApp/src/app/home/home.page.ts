import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ToastController, IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonicModule
  ]
})
export class HomePage implements OnInit {
  movies: any[] = [];

  constructor(private http: HttpClient, private toastController: ToastController) {}

 ngOnInit() {
   // this.loadMovies();
  }
/*
  loadMovies() {
    this.http.get('http://127.0.0.1:8000/mostrarinfo/api/movies/').subscribe({
      next: (data: any) => {
        this.movies = data;
      },
      error: async (err) => {
        const toast = await this.toastController.create({
          message: 'Failed to load movies. Please check your API connection.',
          duration: 2000,
          color: 'danger'
        });
        await toast.present();
        console.error('Error loading movies:', err);
      }
    });
  }

  addToWatchlist(movieId: number) {
    this.http.post('http://127.0.0.1:8000/mostrarinfo/add-to-watchlist/', { movie_id: movieId })
      .subscribe({
        next: async () => {
          const toast = await this.toastController.create({
            message: 'Movie added to your watchlist!',
            duration: 2000,
            color: 'success'
          });
          await toast.present();
        },
        error: async (err) => {
          const toast = await this.toastController.create({
            message: 'Failed to add movie to watchlist.',
            duration: 2000,
            color: 'danger'
          });
          await toast.present();
        }
      });
  }
*/
} 