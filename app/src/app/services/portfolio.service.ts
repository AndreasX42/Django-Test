import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {
  BarController,
  BarElement,
  CategoryScale,
  Chart,
  Legend,
  LinearScale,
  Tooltip,
  LineController,
  LineElement,
  PointElement,
} from 'chart.js';

Chart.register(
  CategoryScale,
  LinearScale,
  BarController,
  BarElement,
  Tooltip,
  Legend,
  LineController,
  LineElement,
  PointElement
);

@Injectable({
  providedIn: 'root',
})
export class PortfolioService {
  private httpClient = inject(HttpClient);
  apiUrl = 'http://localhost:8000/api/portfolio/';

  getPortfolioValues(startDate: string, endDate: string): Observable<any> {
    const params = new HttpParams()
      .set('fecha_inicio', startDate)
      .set('fecha_fin', endDate);

    return this.httpClient.get<any>(this.apiUrl, { params });
  }

  createWeightChart(data: any, chartId: string) {
    const dates = data.values.map((value: any) => value.t);
    const assetClasses = Object.keys(data.values[0].weights);

    const datasets = assetClasses.map((assetClass) => ({
      label: assetClass,
      data: data.values.map((value: any) => value.weights[assetClass]),
      backgroundColor: this.getRandomColor(),
    }));

    return new Chart(chartId, {
      type: 'bar',
      data: {
        labels: dates,
        datasets: datasets,
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          tooltip: {
            mode: 'index',
            intersect: false,
          },
        },
        scales: {
          x: {
            stacked: true,
          },
          y: {
            stacked: true,
            beginAtZero: true,
            title: {
              display: true,
              text: 'Weights',
            },
          },
        },
      },
    });
  }

  createValueChart(data: any, chartId: string) {
    const dates = data.values.map((value: any) => value.t);
    const portfolioValues = data.values.map(
      (value: any) => value.portfolio_value
    );

    return new Chart(chartId, {
      type: 'line',
      data: {
        labels: dates,
        datasets: [
          {
            label: 'Portfolio Value',
            data: portfolioValues,
            borderColor: this.getRandomColor(),
            fill: false,
            tension: 0.1,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          tooltip: {
            mode: 'index',
            intersect: false,
          },
        },
        scales: {
          y: {
            beginAtZero: false,
            title: {
              display: true,
              text: 'Portfolio Value',
            },
          },
        },
      },
    });
  }

  getRandomColor(): string {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }
}
