FROM node:20-alpine3.17

ARG WORK_DIR=/opt/mnt

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

WORKDIR ${WORK_DIR}

COPY package.json package-lock.json ${WORK_DIR}

RUN npm install --omit-dev

COPY . ${WORK_DIR}

RUN npm run build