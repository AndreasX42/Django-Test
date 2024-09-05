import {
  ChangeDetectorRef,
  Component,
  DestroyRef,
  inject,
  signal,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterOutlet } from '@angular/router';
import { PortfolioService } from './services/portfolio.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, FormsModule, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  private destroyRef = inject(DestroyRef);
  private portfolioService = inject(PortfolioService);
  private cdr = inject(ChangeDetectorRef);

  startDate = signal<string>('2022-02-15');
  endDate = signal<string>('2022-03-15');
  portfolioValues = signal<any>(null);

  onSubmit() {
    console.log(this.startDate(), this.endDate());
    this.getPortfolioValues(this.startDate(), this.endDate());
  }

  getPortfolioValues(startDate: string, endDate: string) {
    const sub = this.portfolioService
      .getPortfolioValues(startDate, endDate)
      .subscribe({
        next: (response) => {
          this.portfolioValues.set(response);
          this.cdr.detectChanges();
          this.createCharts();
        },
        complete: () => {
          console.log(this.portfolioValues());
        },
        error: (err) => {
          console.log(err);
        },
      });

    this.destroyRef.onDestroy(() => {
      sub.unsubscribe();
    });
  }

  createCharts() {
    const portfolios = this.portfolioValues().portfolios;

    portfolios.forEach((portfolio: any) => {
      const weightChartId = `weightChart${portfolio.portfolio_id}`;
      const valueChartId = `valueChart${portfolio.portfolio_id}`;

      const weightChartCanvas = document.getElementById(
        weightChartId
      ) as HTMLCanvasElement;
      const valueChartCanvas = document.getElementById(
        valueChartId
      ) as HTMLCanvasElement;

      if (weightChartCanvas && valueChartCanvas) {
        this.portfolioService.createWeightChart(portfolio, weightChartId);

        this.portfolioService.createValueChart(portfolio, valueChartId);
      } else {
        console.error(
          `Canvas elements for charts not found: ${weightChartId}, ${valueChartId}`
        );
      }
    });
  }
}
