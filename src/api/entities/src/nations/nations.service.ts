import { Injectable } from '@nestjs/common';
import { Prisma } from '@prisma/client';
import { DatabaseService } from 'src/database/database.service';

@Injectable()
export class NationsService {
  constructor(private readonly databaseService: DatabaseService){}


  async create(createNationDto: Prisma.nationCreateInput) {
    return this.databaseService.nation.create({ data: createNationDto})
  }

  async findAll() {
    return this.databaseService.nation.findMany({})
  }

  async findOne(id: string) {
    return this.databaseService.nation.findUnique({
      where: {
        id,
      }
    })
  }

  async update(id: string, updateNationDto: Prisma.nationUpdateInput) {
    return this.databaseService.nation.update({
      where: {
        id,
      },
      data: updateNationDto,
    })
  }

  async remove(id: string) {
    return this.databaseService.nation.delete({
      where: {
        id,
      }
    })
  }
}
