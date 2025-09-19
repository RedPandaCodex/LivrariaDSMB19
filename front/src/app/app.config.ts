import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { tokenInterceptor } from './auth/token.inteceptor';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideZonelessChangeDetection } from '@angular/core';
// import { provideBrowserGlobalErrorListeners } from '@angular/platform-browser';


export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(), 
    // Conecta o Angular aos erros globais do navegador (window.onerror, unhandledrejection),
    // encaminhando-os para o sistema de erro do Angular (ErrorHandler). Útil para logs/monitoramento.

    provideZonelessChangeDetection(), 
    // Ativa detecção de mudanças sem Zone.js. Deixa a UI reagir via sinais/inputs/efeitos do Angular,
    // reduz overhead de change detection e dá mais previsibilidade de quando a tela atualiza.

    provideRouter(routes),
    // Registra o roteador da aplicação com o conjunto de rotas definido em `routes`.
    // Habilita navegação SPA (links, guards, resolvers, lazy-loading, etc.).

    provideClientHydration(withEventReplay()),
    // Hidrata no cliente o HTML renderizado no servidor (SSR). O `withEventReplay()` captura cliques/teclas
    // antes da hidratação e os “reexecuta” depois, evitando perda de interações durante o boot do app.

    provideHttpClient(withInterceptors([tokenInterceptor])),
    // Disponibiliza o HttpClient globalmente para requisições HTTP (GET/POST/PUT/DELETE, interceptors, etc.).
  ],
};







