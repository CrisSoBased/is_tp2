import { Injectable } from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { DatabaseService } from 'src/database/database.service';

@Injectable()
export class ClubsService {
  constructor(private readonly databaseService: DatabaseService){}


  async create(createClubDto: Prisma.clubCreateInput) {
    return this.databaseService.club.create({ data: createClubDto})
  }

  async findAll() {
    return this.databaseService.club.findMany({})
  }

  async findOne(id: string) {
    return this.databaseService.club.findUnique({
      where: {
        id,
      }
    })
  }

  async update(id: string, updateClubDto: Prisma.clubUpdateInput) {
    return this.databaseService.club.update({
      where: {
        id,
      },
      data: updateClubDto,
    })
  }

  async remove(id: string) {
    return this.databaseService.club.delete({
      where: {
        id,
      }
    })
  }
}
